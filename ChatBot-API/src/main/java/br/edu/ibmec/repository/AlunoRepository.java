package br.edu.ibmec.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import br.edu.ibmec.models.Aluno;

@Repository
public interface AlunoRepository extends JpaRepository<Aluno, Long> {

}