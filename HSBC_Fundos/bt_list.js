var _BTS=[
["alterarestipulante","Alterar Estipulante"],
["alterarsenha","Alterar Senha"],
["cartacredito","Carta de Cr&eacute;dito"],
["demonstrativoir","Demonstrativo I.R."],
["descadastrartodos","Descadastrar todos"],
["extratoconsolidado","Extrato consolidado"],
["faleconosco","Fale conosco"],
["gerente","Fale conosco"],
["gravararquivo","Gravar arquivo"],
["nao","N&atilde;o"],
["novaaplicacao","Nova aplica&ccedil;&atilde;o"],
["novacompra","Nova compra"],
["novacontratacao","Nova contrata&ccedil;&atilde;o"],
["novasenha","Nova senha"],
["novatransf","Nova transfer&ecirc;ncia"],
["novodoc","Novo DOC"],
["novoinvestimento","Novo investimento programado"],
["novopag","Novo pagamento"],
["novoresgate","Novo resgate"],
["outraconta","Outra conta"],
["primeiratela","Primeira tela"],
["proxima","Pr&oacute;xima"],
["quick","Quicken/Money"],
["simulacao","Simula&ccedil;&atilde;o"],
["solicpremio","Solicita&ccedil;&atilde;o de premia&ccedil;&atilde;o"],
["ultima","&Uacute;ltima"],
["viacorreio","Via correio"],
["consultarpropostas","Consultar propostas"],
["enviarproposta","Enviar proposta de cr&eacute;dito"],
["imprimirconsulta","Imprimir consulta"],
["imprimircontrato","Imprimir contrato"],
["visualizarparecer","Parecer da cr&eacute;dito"],
["visualizarprop","Visualizar proposta"],
["imprimirdocumentos","Imprimir documentos"],
["iniciarproposta","Iniciar proposta de cr&eacute;dito"]
];
function getLabelText(lb){
  lb=String(lb);
  for(i=0;i<_BTS.length;i++)if(_BTS[i][0]==lb.replace(/^\s+/,"").replace(/\s+$/,""))return _BTS[i][1];
  return lb.charAt(0).toUpperCase()+lb.substring(1);
}
