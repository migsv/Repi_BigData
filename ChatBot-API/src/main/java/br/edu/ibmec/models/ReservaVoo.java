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

    @Column
    private String companhiaAerea;
    
    @Column(nullable = false)
    private String origem;
    
    @Column(nullable = false)
    private String destino;
    
    @Column(nullable = false)
    private LocalDateTime dataPartida;
    
    @Column
    private LocalDateTime dataRetorno;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal preco;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private StatusReserva status = StatusReserva.PENDENTE;
    
    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }

    // Construtores, getters e setters podem ser gerados pelo Lombok (@Data)
}