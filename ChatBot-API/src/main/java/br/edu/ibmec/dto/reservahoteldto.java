package br.edu.ibmec.dto;

public record reservahoteldto(
    Long id,
    usuariodto usuario,
    String nomeHotel,
    String codigoApiHotel,
    String localizacao,
    String dataCheckIn,
    String dataCheckOut,
    String precoTotal,
    String status,
    String dataCriacao
) {
}
