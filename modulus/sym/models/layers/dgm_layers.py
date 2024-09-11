# SPDX-FileCopyrightText: Copyright (c) 2023 - 2024 NVIDIA CORPORATION & AFFILIATES.
# SPDX-FileCopyrightText: All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Optional, Union

import paddle
import paddle.nn as nn
from paddle import Tensor

from modulus.sym.models.activation import Identity, get_activation_fn
from modulus.sym.models.layers.weight_norm import WeightNormLinear


class DGMLayer(nn.Layer):
    """
    Deep Galerkin Model layer.

    Parameters
    ----------
    in_features_1 : int
        Number of input features for first input.
    in_features_2 : int
        Number of input features for second input.
    out_features : int
        Number of output features.
    activation_fn : Union[nn.Layer, Callable[[Tensor], Tensor]], optional
        Activation function, by default Activation.IDENTITY
    weight_norm : bool, optional
        Apply weight normalization, by default False
    activation_par : Optional[nn.Parameter], optional
        Activation parameter, by default None

    Notes
    -----
    Reference: DGM: A deep learning algorithm for solving partial differential
    equations, https://arxiv.org/pdf/1708.07469.pdf
    """

    def __init__(
        self,
        in_features_1: int,
        in_features_2: int,
        out_features: int,
        activation_fn: Union[nn.Layer, Callable[[Tensor], Tensor], None] = None,
        weight_norm: bool = False,
        activation_par: Optional[paddle.Tensor] = None,
    ) -> None:
        super().__init__()

        if activation_fn is None:
            self.activation_fn = Identity()
        else:
            self.activation_fn = get_activation_fn(activation_fn)
        self.weight_norm = weight_norm
        self.activation_par = activation_par

        if weight_norm:
            self.linear_1 = WeightNormLinear(in_features_1, out_features, bias=False)
            self.linear_2 = WeightNormLinear(in_features_2, out_features, bias=False)
        else:
            self.linear_1 = nn.Linear(in_features_1, out_features, bias_attr=False)
            self.linear_2 = nn.Linear(in_features_2, out_features, bias_attr=False)
        self.bias = self.create_parameter(
            [out_features],
            default_initializer=nn.initializer.Constant(0),
        )
        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.initializer.XavierUniform()(self.linear_1.weight)
        nn.initializer.XavierUniform()(self.linear_2.weight)
        nn.initializer.Constant(0.0)(self.bias)
        if self.weight_norm:
            nn.initializer.Constant(1.0)(self.linear_1.weight_g)
            nn.initializer.Constant(1.0)(self.linear_2.weight_g)

    def forward(self, input_1: Tensor, input_2: Tensor) -> Tensor:
        x = self.linear_1(input_1) + self.linear_2(input_2) + self.bias

        if self.activation_fn is not None:
            if self.activation_par is None:
                x = self.activation_fn(x)
            else:
                x = self.activation_fn(self.activation_par * x)
        return x
