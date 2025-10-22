package br.edu.ibmec.models;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class ReservaVoo {

    private Long id;

    private String companhiaAerea;
    
    private String origem;
    
    private String destino;
    
    private LocalDateTime dataPartida;
    
    private LocalDateTime dataRetorno;
    
    private BigDecimal preco;
    
    @Column(nullable = false)
    private StatusReserva status = StatusReserva.PENDENTE;
    
    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}