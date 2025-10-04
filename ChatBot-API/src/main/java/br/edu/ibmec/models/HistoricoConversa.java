package br.edu.ibmec.models;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
public class HistoricoConversa {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;
    
    @Column(nullable = false, length = 1000)
    private String mensagemUsuario;
    
    @Column(nullable = false, length = 1000)
    private String respostaBot;
    
    @Column
    private String intencaoReconhecida;
    
    @Enumerated(EnumType.STRING)
    private Sentimento sentimento;
    
    @Column(nullable = false)
    private LocalDateTime dataHora = LocalDateTime.now();
    
    public enum Sentimento {
        POSITIVO, NEUTRO, NEGATIVO
    }
}