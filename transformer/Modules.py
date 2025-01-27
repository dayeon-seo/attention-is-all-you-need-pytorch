import torch
import torch.nn as nn
import torch.nn.functional as F # PyTorch의 함수 계산을 할 수 있게 해주는 모듈이다.

__author__ = "Yu-Hsiang Huang" # 저자~

class ScaledDotProductAttention(nn.Module): # Scaled Dot-ProductAttention을 구현한다. 쿼리, 키, 값을 이용하여 가중치를 계산한다.
    # 어텐션 스코어는 쿼리와 키 사이의 유사도를 나타내는 값이다.
    ''' Scaled Dot-Product Attention ''' 

    def __init__(self, temperature, attn_dropout=0.1):
        super().__init__()
        self.temperature = temperature # 기울기 소실 문제를 해결하기 위하여 temperature가 필요하다.
        self.dropout = nn.Dropout(attn_dropout)

    def forward(self, q, k, v, mask=None):

        attn = torch.matmul(q / self.temperature, k.transpose(2, 3)) # 어텐션 스코어를 계산한다.

        if mask is not None:
            attn = attn.masked_fill(mask == 0, -1e9) # 마스크를 적용한다.

        attn = self.dropout(F.softmax(attn, dim=-1)) # 드롭아웃을 적용한다. softmax 함수로 어텐션 가중치를 계산한다.
        output = torch.matmul(attn, v) # 가중합을 통해서 어텐션 결과를 적용한다.

        return output, attn
