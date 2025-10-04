package br.edu.ibmec.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record reservavoodto(
    Long id,
    usuariodto usuario,
    String companhiaAerea,
    String origem,
    String destino,
    LocalDateTime dataPartida,
    LocalDateTime dataRetorno,
    BigDecimal preco,
    String status
) {
    
}
