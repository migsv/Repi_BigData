package br.edu.ibmec.dto;

public record historicoconversadto(
    Long id,
    usuariodto usuario,
    String mensagemUsuario,
    String respostaBot,
    String intencaoReconhecida,
    String sentimento,
    String dataHora
) {
}
