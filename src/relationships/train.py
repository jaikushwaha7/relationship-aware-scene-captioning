import json
import torch
from torch.utils.data import Dataset, DataLoader
from model import RelationshipGNN

RELATIONS = [
    "left of", "right of", "in front of", "behind",
    "on top of", "under", "inside", "around", "over", "next to"
]

rel2idx = {r: i for i, r in enumerate(RELATIONS)}

class RelDataset(Dataset):
    def __init__(self, path):
        self.data = json.load(open(path))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        d = self.data[idx]
        return (
            torch.tensor(d["subject"]["class"]),
            torch.tensor(d["subject"]["bbox"], dtype=torch.float),
            torch.tensor(d["object"]["class"]),
            torch.tensor(d["object"]["bbox"], dtype=torch.float),
            torch.tensor(rel2idx[d["predicate"]])
        )

def main():
    dataset = RelDataset("data/processed/relationships/relationship_pairs.json")
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    model = RelationshipGNN(num_classes=150, num_relations=len(RELATIONS))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(15):
        total = 0
        for s_cls, s_box, o_cls, o_box, y in loader:
            logits = model(s_cls, s_box, o_cls, o_box)
            loss = loss_fn(logits, y)

            opt.zero_grad()
            loss.backward()
            opt.step()
            total += loss.item()

        print(f"Epoch {epoch}: {total/len(loader):.4f}")

    torch.save(model.state_dict(), "models/relationship_predictor/gnn.pt")

if __name__ == "__main__":
    main()
