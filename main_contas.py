from classe_conta import Conta
from classe_cc import ContaCor
from classe_pp import ContaPP

c2= ContaCor("Maria", 4000, 1000)
c3= ContaPP("José", 3000, 0.5)

c2.extrato()
print(f"{c3.render_juros()}")