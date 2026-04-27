# ✅ AISA Clean Django App — Negative Training Dataset

> A **fully secure** Django REST API. Zero intentional vulnerabilities.
> Used by AISA as a **negative training example** — any detection here = false positive.

---

## 🎯 Purpose

| Repo | Expected Score | Expected Severity | Purpose |
|------|---------------|-------------------|---------|
| `vuln_django_app` | 100 | Critical | Positive training — detect everything |
| `clean_django_app` | < 10 | Low | **Negative training — detect nothing** |
| `medium_django_app` | ~50 | Medium/High | Boundary training |

---

## 🔒 Fixes Applied

Every vulnerability from `vuln_django_app` has a corresponding fix here:

| # | Was (vuln repo) | Now (clean repo) |
|---|----------------|-----------------|
| 1 | `Order.objects.get(id=id)` | `get_object_or_404(Order, id=id, user=request.user)` |
| 2 | No `permission_classes` | `permission_classes = [IsAuthenticated]` globally |
| 3 | `fields = "__all__"` | `fields = ["id", "phone"]` — explicit safe fields only |
| 4 | `OrderSerializer(data=request.data)` | Separate `OrderCreateSerializer`, user from `request.user` |
| 5 | Admin endpoint, no guard | `permission_classes = [IsAdminUser]` |
| 6 | `return Response({"token": token})` | `TokenAuthentication` validates; token never echoed |

---

## 📁 Structure

```
clean_django_app/
├── api/
│   ├── models.py         # Clean models — no PII, no sensitive fields
│   ├── serializers.py    # Explicit field lists, read_only enforced
│   ├── views.py          # All fixes applied, documented inline
│   └── urls.py           # All endpoints require auth
├── aisa_labels.json      # ML labels — vulnerabilities: [], fixes_applied: [6]
└── manage.py
```

---

## 🤖 AISA Expected Output

```json
{
  "overall_risk": 5.0,
  "severity": "Low",
  "vulnerabilities_detected": [],
  "attack_chains": []
}
```

If AISA detects anything here → **false positive** → use `aisa_labels.json` fixes to retrain.

Webhook test marker: 2026-04-20
Webhook test marker 2: 2026-04-20
Webhook test marker 3: 2026-04-27
Webhook test marker 4: 2026-04-28
Webhook test marker 4: 2026-04-28
---

## 🛠 Setup

```bash
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```
