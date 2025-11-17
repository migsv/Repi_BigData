package br.edu.ibmec.controllers;

import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @GetMapping
    public Iterable<Usuario> getAllUsuarios() {
        List<Usuario> usuarios = new ArrayList<>();
        usuarioRepository.findAll().forEach(usuarios::add);
        return usuarios;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Usuario> getUsuarioById(@PathVariable String id) {
        Optional<Usuario> usuario = usuarioRepository.findById(id);
        return usuario.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/cpf/{cpf}")
    public ResponseEntity<Usuario> getUsuarioByCpf(@PathVariable String cpf) {
        Optional<Usuario> usuario = usuarioRepository.findByCpf(cpf);
        return usuario.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Usuario> createUsuario(@RequestBody Usuario usuario) {
        String cpf = Optional.ofNullable(usuario.getCpf())
                .map(String::trim)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "CPF é obrigatório."));

        usuarioRepository.findByCpf(cpf).ifPresent(existing -> {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Usuário já cadastrado para este CPF.");
        });

        usuario.setId(UUID.randomUUID().toString());
        usuario.setCpf(cpf);
        Usuario savedUsuario = usuarioRepository.save(usuario);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUsuario);
    }
}
