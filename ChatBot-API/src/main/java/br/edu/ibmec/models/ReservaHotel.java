package br.edu.ibmec.models;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Entity
public class ReservaHotel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;
    
    @Column(nullable = false)
    private String nomeHotel;
    
    @Column
    private String codigoApiHotel;
    
    @Column(nullable = false)
    private String localizacao;
    
    @Column(nullable = false)
    private LocalDate dataCheckIn;
    
    @Column(nullable = false)
    private LocalDate dataCheckOut;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal precoTotal;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private StatusReserva status = StatusReserva.PENDENTE;
    
    @Column(nullable = false)
    private LocalDateTime dataCriacao = LocalDateTime.now();
    
    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}