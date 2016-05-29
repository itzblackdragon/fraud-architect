# Fraud Architect
A fake data generator for creating datasets that model patterns of fraudulent behavior.

## Philosophy
There are lots of fake data generators out there. But none of them are suited to generating fake audit logs or models of other transactional relationships.

This one models both legitimate and fraudulent user activity based on cases seen in the field, which makes it ideal for testing fraud detection/auditing appliances and machine learning algorithms.

How well can your black box tell the difference between normal and anomalous user behavior?

## Current Status
Heavily in alpha. Expect soul-breaking changes often.

## Notes
Be careful running this script in Pypy. By default it writes to a file in the /resources directory and will quickly surpass 1GB in size in a matter of seconds. I have hard-capped result output at 10,000 transactions (4MB). User-configurable parameters will come later.