package br.edu.ibmec.dto;

public record reservavoodto(
    Long id,
    usuariodto usuario,
    String nomeVoo,
    String codigoApiVoo,
    String origem,
    String destino,
    String dataPartida,
    String dataRetorno,
    String precoTotal,
    String status,
    String dataCriacao
) {
    
}
