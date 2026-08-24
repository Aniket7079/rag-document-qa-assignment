# Sample Q&A Log

Representative validation questions grounded in the supplied corpus. The exact wording of LLM responses may vary, but the facts and sources should remain grounded in the documents.

## 1. How many PTO days can a full-time employee accrue per year?

Full-time employees accrue 1.75 days of PTO per month, up to a maximum of 21 days per calendar year.

**Sources:** Employee_Handbook.pdf - page 2 - `Employee_Handbook_p2_c1`

## 2. How long does a password reset link remain valid?

The password reset link expires after 24 hours.

**Sources:** FAQ_Support.pdf - page 2 - `FAQ_Support_p2_c1`

## 3. What is the Standard plan monthly price and included storage?

The Standard plan costs $12 per user per month and includes 500 GB of pooled storage, for up to 25 users.

**Sources:** Pricing_and_SLA.pdf - page 2 - `Pricing_and_SLA_p2_c1`

## 4. What is the uptime guarantee for the Enterprise plan?

The Enterprise plan has a 99.95% monthly uptime guarantee.

**Sources:** Pricing_and_SLA.pdf - page 2 - `Pricing_and_SLA_p2_c1`

## 5. How long are deleted CloudSync Pro files retained?

Deleted files are retained in the Recovery Bin for 30 days before permanent removal, unless Legal Hold is enabled, in which case retention is indefinite until Legal Hold is disabled by an administrator.

**Sources:** Product_Manual.pdf - page 3 - `Product_Manual_p3_c1`

## 6. What should I do if the CloudSync Pro LED is blinking red?

The likely cause is a degraded storage array. Replace the failed drive bay indicated in the app; RAID will automatically rebuild.

**Sources:** Product_Manual.pdf - page 3 - `Product_Manual_p3_c1`

## 7. What is required to access Restricted Data?

Restricted Data access requires named individuals plus Data Custodian and Security team approval. The policy also requires hardware security key MFA; password-only or SMS-based MFA is not sufficient.

**Sources:** Security_Policy.pdf - page 2 - `Security_Policy_p2_c1`

## 8. How soon before a new employee starts does IT provision email, Slack, and GitHub?

IT provisions email, Slack, and GitHub accounts 2 business days before the start date.

**Sources:** Onboarding_Guide.pdf - page 3 - `Onboarding_Guide_p3_c1`

## 9. What is the API endpoint for uploading a file?

The file upload endpoint is `POST /v2/files` and it uses `multipart/form-data`. The required parameter is `file`; `folder_id` and `overwrite` are optional.

**Sources:** API_Reference.pdf - page 2 - `API_Reference_p2_c1`

## 10. What happens when the API rate limit is exceeded?

The API returns HTTP 429 Too Many Requests with a `Retry-After` header indicating how many seconds remain until the limit resets.

**Sources:** API_Reference.pdf - page 2 - `API_Reference_p2_c1`

## 11. What is Atman Cloud's office address in Mumbai?

I could not find the answer in the provided documents.

**Expected behavior:** Abstain because the supplied documents do not contain an office address in Mumbai.

## 12. Does the company offer a free laptop to every employee?

I could not find the answer in the provided documents.

**Expected behavior:** Abstain because the supplied documents mention laptop shipping and IT provisioning, but do not define a free-laptop benefit.
