package br.edu.ibmec.models;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
public class ReservaVoo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;
    
    @Column(nullable = false)
    private String origem;
    
    @Column(nullable = false)
    private String destino;
    
    @Column(nullable = false)
    private LocalDateTime dataHoraIda;
    
    @Column
    private LocalDateTime dataHoraVolta;
    
    @Column
    private String companhiaAerea;
    
    @Column
    private String numeroVoo;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal preco;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private StatusReserva status = StatusReserva.PENDENTE;
    
    @Column(nullable = false)
    private LocalDateTime dataCriacao = LocalDateTime.now();
    
    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}