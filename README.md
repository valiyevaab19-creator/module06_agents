## Week 10 Mini-Project

My mini-project is a mock appointment assistant for a small office. It can look up available appointment times for Monday, Wednesday, and Friday using a separate tool class. The assistant is a mock because its schedule is stored in a Python dictionary and its responses use simple keyword rules instead of a real AI model. Booking, cancelling, and rescheduling requests are passed to a person because those actions change the schedule. If this assistant used real customer data, incorrect or exposed appointment information could create privacy and scheduling problems.

Week 11 - Local Model

The model answered the office location correctly using the facts in its instructions. It also correctly explained what a customer should bring to an appointment. When I asked whether the office does business taxes, it said that it did not know and directed me to the front desk. I kept appointment times and schedule changes in code because those answers need to be reliable and should not be invented by the model. The model is used only for questions that are not already handled by the program’s rules.