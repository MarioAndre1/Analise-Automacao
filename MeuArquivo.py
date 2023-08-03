import pandas as pd
import win32com.client as win32

tabela_vendas = pd.read_excel('Vendas.xlsx')

pd.set_option('display.max_columns', None)

faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()

quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()

ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})

print(quantidade)
print(faturamento)
print('-'*50)
print(ticket_medio)

# envio do relatório
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'marioandredutra@hotmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Atte.,</p>
<p>Mario Bertollo</p>
'''

mail.Display()

print('Email Enviado')