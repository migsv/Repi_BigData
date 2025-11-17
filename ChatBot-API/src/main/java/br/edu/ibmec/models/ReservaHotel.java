package br.edu.ibmec.models;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Container(containerName = "ReservasHotel")
public class ReservaHotel {

    @Id
    private String id;

    @PartitionKey
    private String usuarioId;

    private String usuarioCpf;

    private String nomeHotel;

    private String localizacao;

    private LocalDate dataCheckIn;

    private LocalDate dataCheckOut;

    private BigDecimal precoTotal;

    private StatusReserva status = StatusReserva.CONFIRMADA;

    private LocalDateTime dataCriacao = LocalDateTime.now();

    public enum StatusReserva {
        PENDENTE, CONFIRMADA, CANCELADA
    }
}
