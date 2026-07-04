# مرجع بيئة Odoo الإنتاجية

**تاريخ التوثيق:** 2026-07-04

## 1. معلومات الخادم

- المستخدم: `helioit`
- نظام التشغيل: Linux (بناءً على بيئة التشغيل)
- قاعدة البيانات: PostgreSQL
- قاعدة البيانات المستخدمة فعلياً: `production`

---

## 2. ملف إعدادات Odoo

مسار ملف الإعدادات:

```text
/etc/odoo/odoo.conf
```

إعداد مسارات الإضافات:

```text
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/opt/odoo/custom-addons
```

### شرح المسارات

#### إضافات Odoo القياسية

```text
/usr/lib/python3/dist-packages/odoo/addons
```

تحتوي على الوحدات الرسمية القياسية الخاصة بـ Odoo.

#### الإضافات المخصصة

```text
/opt/odoo/custom-addons
```

تحتوي على جميع الوحدات المخصصة والإضافات الخارجية المستخدمة داخل النظام.

---

## 3. قواعد البيانات الموجودة على الخادم

```text
eslam-test
per
perr
pro1
pro2
production
production2026
productionbd
test
testdd
train
tt
```

### قاعدة الإنتاج الحالية

```text
production
```

---

## 4. الوحدات المخصصة الموجودة على الخادم

```text
account_reconcile_model_oca
account_reconcile_oca
account_statement_base
advanced_web_domain_widget
app_common
app_odoo_customize
base_account_budget
base_accounting_kit
deltatech_stock_negative
eqp_backups
hr_gantt
hr_payroll
hr_payroll_account_community
hr_work_entry_contract_enterprise
invoice_by_journal_users
l10n_eg_hr_payroll
l10n_eg_hr_payroll_account_community
payments_internal_transfer
payslip_bill_grouping_18
pos_order_number
pos_order_payment_split
pos_receipt_extend
pos_user_disable_buttons
QR_code_in_pos_receipt
simplify_access_management
stock_internal_transfer_two_step
warehouse_by_users
web_gantt
web_responsive
```

إجمالي الوحدات الموجودة: **29 وحدة**.

---

## 5. الوحدات المخصصة المثبتة فعلياً في قاعدة production

```text
advanced_web_domain_widget
base_account_budget
base_accounting_kit
deltatech_stock_negative
eqp_backups
hr_gantt
hr_payroll
hr_payroll_account_community
hr_work_entry_contract_enterprise
invoice_by_journal_users
l10n_eg_hr_payroll
l10n_eg_hr_payroll_account_community
payments_internal_transfer
pos_order_number
pos_order_payment_split
pos_receipt_extend
pos_user_disable_buttons
QR_code_in_pos_receipt
simplify_access_management
warehouse_by_users
web_gantt
web_responsive
```

إجمالي الوحدات المثبتة: **22 وحدة**.

---

## 6. الوحدات الموجودة ولكن غير مثبتة

```text
account_reconcile_model_oca
account_reconcile_oca
account_statement_base
app_common
app_odoo_customize
payslip_bill_grouping_18
stock_internal_transfer_two_step
```

---

## 7. تصنيف الوحدات المثبتة حسب الوظيفة

### المحاسبة والمالية

```text
base_account_budget
base_accounting_kit
invoice_by_journal_users
payments_internal_transfer
```

#### الوصف
- إدارة الموازنات.
- تحسين وظائف المحاسبة.
- تقييد الفواتير حسب المستخدم.
- التحويلات الداخلية بين الحسابات.

### الموارد البشرية والرواتب

```text
hr_gantt
hr_payroll
hr_payroll_account_community
hr_work_entry_contract_enterprise
l10n_eg_hr_payroll
l10n_eg_hr_payroll_account_community
```

#### الوصف
- إدارة الرواتب.
- تخصيص رواتب مصر.
- التكامل المحاسبي للرواتب.
- عقود وسجلات العمل.
- عرض جانت للموارد البشرية.

### المخزون والمستودعات

```text
deltatech_stock_negative
warehouse_by_users
```

#### الوصف
- التحكم في المخزون السالب.
- تقييد المستودعات حسب المستخدم.

### نقاط البيع POS

```text
pos_order_number
pos_order_payment_split
pos_receipt_extend
pos_user_disable_buttons
QR_code_in_pos_receipt
```

#### الوصف
- تخصيص أرقام الطلبات.
- تقسيم المدفوعات.
- تخصيص الإيصالات.
- إخفاء أو تعطيل أزرار معينة.
- إضافة QR Code على الإيصالات.

### الإدارة والصلاحيات

```text
simplify_access_management
eqp_backups
```

#### الوصف
- إدارة مبسطة للصلاحيات.
- النسخ الاحتياطي.

### واجهة المستخدم

```text
advanced_web_domain_widget
web_gantt
web_responsive
```

#### الوصف
- تخصيص البحث والفلاتر.
- مخططات Gantt.
- تحسين توافق الواجهة مع الشاشات المختلفة.

---

## 8. أوامر مرجعية مفيدة

### عرض الإضافات المعرفة في Odoo

```bash
sudo grep addons_path /etc/odoo/odoo.conf
```

### عرض قواعد البيانات

```bash
sudo -u postgres psql -l
```

### عرض الوحدات المثبتة

```bash
sudo -u postgres psql -d production -c "SELECT name FROM ir_module_module WHERE state='installed';"
```

### عرض الوحدات المخصصة الموجودة

```bash
ls -1 /opt/odoo/custom-addons
```

---

## 9. ملاحظات مهمة للترقية أو النسخ الاحتياطي

1. الاحتفاظ بنسخة من قاعدة بيانات `production` قبل أي تحديث.
2. الاحتفاظ بنسخة كاملة من:

```text
/opt/odoo/custom-addons
```

3. مراجعة توافق الوحدات المخصصة قبل أي ترقية مستقبلية.
4. توثيق أي تعديلات جديدة تضاف إلى مجلد `custom-addons`.
5. بعد أي ترقية يجب اختبار:
   - الرواتب.
   - المحاسبة.
   - نقاط البيع.
   - الصلاحيات.
   - المستودعات.

---

## 10. ملخص تنفيذي

- قاعدة الإنتاج: `production`
- ملف الإعدادات: `/etc/odoo/odoo.conf`
- مجلد الوحدات المخصصة: `/opt/odoo/custom-addons`
- عدد الوحدات المخصصة الموجودة: 29
- عدد الوحدات المخصصة المثبتة: 22
- أهم الأنظمة المخصصة المستخدمة:
  - الرواتب المصرية.
  - المحاسبة والموازنات.
  - نقاط البيع.
  - الصلاحيات.
  - المستودعات.
  - النسخ الاحتياطي.
