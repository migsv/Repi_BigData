package br.edu.ibmec.models;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Container(containerName = "ReservasVoo")
public class ReservaVoo {

    @Id
    private String id;

    @PartitionKey
    private String usuarioId;

    private String usuarioCpf;

    private String companhiaAerea;
    
    private String origem;

    private String destino;

    private LocalDateTime dataPartida;

    private LocalDateTime dataRetorno;

    private BigDecimal preco;

    private StatusReserva status = StatusReserva.CONFIRMADA;

    private LocalDateTime dataCriacao = LocalDateTime.now();

    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}
