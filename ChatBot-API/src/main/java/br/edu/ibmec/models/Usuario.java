package br.edu.ibmec.models;

import org.springframework.data.annotation.Id;

import lombok.Data;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

import java.util.List;

@Data
@Container(containerName = "Usuarios")
public class Usuario {
  
    @Id
    private String id;

    @PartitionKey
    private String cpf;

    private String nome;
    
    private String email;
    
    private String telefone;
    
    private List<ReservaVoo> reservasVoo;
    private List<ReservaHotel> reservasHotel;

}