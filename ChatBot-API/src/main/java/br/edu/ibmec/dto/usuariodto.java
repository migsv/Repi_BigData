package br.edu.ibmec.dto;

public record usuariodto(
    Long id,
    String nome,
    String email,
    String telefone,
    String idioma,
    String moeda
) {

    public long getId() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getId'");
    }

    public String getNome() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getNome'");
    }}