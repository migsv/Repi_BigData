package br.edu.ibmec.controllers;

import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
        return usuarioRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Usuario> getUsuarioById(@PathVariable Long id) {
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

        Optional<Usuario> existingUsuario = usuarioRepository.findByCpf(usuario.getCpf());
        if (existingUsuario.isPresent()) {
            return ResponseEntity.ok(existingUsuario.get());
        }

        usuario.setId(UUID.randomUUID().toString());
        Usuario savedUsuario = usuarioRepository.save(usuario);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUsuario);
    }
}