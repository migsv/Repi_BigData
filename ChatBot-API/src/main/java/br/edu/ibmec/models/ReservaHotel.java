package br.edu.ibmec.models;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;


@Data
public class ReservaHotel {
    @Id
    private Long id;
    
    private String nomeHotel;
    
    private String codigoApiHotel;
    
    private String localizacao;
    
    private LocalDate dataCheckIn;
    
    private LocalDate dataCheckOut;
    
    private BigDecimal precoTotal;
    
    private StatusReserva status = StatusReserva.PENDENTE;
    
    private LocalDateTime dataCriacao = LocalDateTime.now();
    
    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}