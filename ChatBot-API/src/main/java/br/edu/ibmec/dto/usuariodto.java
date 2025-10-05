package br.edu.ibmec.dto;

public record usuariodto(
    Long id,
    String nome,
    String email,
    String telefone,
    String idioma,
    String moeda
) { }
