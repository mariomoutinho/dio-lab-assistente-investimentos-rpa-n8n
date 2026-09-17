# Como executar a integração RPA + n8n

## 1. Importar o workflow

No n8n:

1. Abra **Workflows**.
2. Selecione **Import from File**.
3. Escolha `n8n/workflow.json`.
4. Abra o nó **Receber clientes** e copie a URL do Webhook.

## 2. Escolher a URL correta

- **Teste local:** o Python precisa rodar na mesma máquina do n8n. Use a URL **Test URL** e clique em **Listen for test event** antes de executar o Python.
- **Google Colab:** não use `http://localhost:5678`. Use n8n Cloud ou uma URL pública de túnel.
- **Produção:** ative o workflow e use a **Production URL**.

A URL de teste normalmente termina em:

```
/webhook-test/clientes
```

A URL de produção normalmente termina em:

```
/webhook/clientes
```

## 3. Executar o RPA

Abra `rpa/extrair_clientes.py`, substitua:

```python
N8N_WEBHOOK = "COLE_AQUI_A_URL_DO_WEBHOOK"
```

pela URL copiada do n8n e execute o arquivo. No Colab, cole as células do mesmo código e execute depois de colocar a URL pública.

## 4. Payload enviado

O Python envia:

```json
{
  "clientes": [
    {
      "nome": "Ana Silva",
      "email": "ana@email.com",
      "saldo": "R$ 12.500,00",
      "perfil": "Conservador"
    }
  ]
}
```

O workflow valida a lista, gera uma recomendação por perfil e devolve um JSON com `status`, `total` e `clientes`.

## 5. Erros comuns

### Nenhum evento aparece

O Webhook está escutando a URL de teste, mas o Python está usando outra URL, ou `localhost` está sendo executado em ambientes diferentes.

### 404

O workflow não está ativo quando a URL de produção é usada, ou o caminho do Webhook não é `clientes`.

### 405

O método configurado é diferente de POST. O nó deve estar configurado com **HTTP Method: POST**.

### 400

O corpo não contém a propriedade `clientes` como uma lista. Use o código fornecido neste projeto.
