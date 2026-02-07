import torch
import torch.nn as nn
import torch.nn.functional as F

class RelationshipGNN(nn.Module):
    def __init__(self, num_classes, num_relations, emb_dim=64):
        super().__init__()

        self.obj_embed = nn.Embedding(num_classes, emb_dim)

        self.fc = nn.Sequential(
            nn.Linear(emb_dim * 2 + 8, 256),
            nn.ReLU(),
            nn.Linear(256, num_relations)
        )

    def forward(self, subj_cls, subj_box, obj_cls, obj_box):
        subj_emb = self.obj_embed(subj_cls)
        obj_emb = self.obj_embed(obj_cls)

        x = torch.cat([subj_emb, obj_emb, subj_box, obj_box], dim=1)
        return self.fc(x)
