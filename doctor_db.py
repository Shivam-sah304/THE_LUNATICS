
name, phone, email, address, dob, desc, degree, experience, specialization = [[] for _ in range(9)]


def doctor_registeration(**kwargs):
  name.append(kwargs['name'])
  phone.append(kwargs['phone'])


def doctor_valdation(**kwargs):
  print(name)