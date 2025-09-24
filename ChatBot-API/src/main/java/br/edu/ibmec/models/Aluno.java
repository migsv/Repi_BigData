package br.edu.ibmec.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Data;

@Data
@Entity
public class Aluno {
    @Id
    private Long id;
    
    @Column
    private String nome;
    
    @Column
    private String matricula;
    
    @Column
    private String email;
    
    @Column
    private String cpf;
    
    @Column
    private String telefone;
}
