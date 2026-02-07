from sklearn.metrics import classification_report
import torch

def evaluate(model, loader):
    y_true, y_pred = [], []

    with torch.no_grad():
        for s_cls, s_box, o_cls, o_box, y in loader:
            logits = model(s_cls, s_box, o_cls, o_box)
            y_true.extend(y.tolist())
            y_pred.extend(logits.argmax(dim=1).tolist())

    print(classification_report(y_true, y_pred))
