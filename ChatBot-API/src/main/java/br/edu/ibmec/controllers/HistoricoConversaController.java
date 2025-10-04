package br.edu.ibmec.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.edu.ibmec.models.HistoricoConversa;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.HistoricoConversaRepository;
import br.edu.ibmec.repository.UsuarioRepository;

@RestController
@RequestMapping("/historico-conversas")
public class HistoricoConversaController {

    @Autowired
    private HistoricoConversaRepository historicoConversaRepository;
    
    @Autowired
    private UsuarioRepository usuarioRepository;

    @GetMapping
    public ResponseEntity<List<HistoricoConversa>> getHistoricoConversas() {
        return ResponseEntity.ok(historicoConversaRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<HistoricoConversa> getHistoricoConversa(@PathVariable Long id) {
        Optional<HistoricoConversa> historico = historicoConversaRepository.findById(id);
        return historico.map(ResponseEntity::ok)
                       .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<HistoricoConversa>> getHistoricoByUsuario(@PathVariable Long usuarioId) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        List<HistoricoConversa> historico = historicoConversaRepository.findByUsuarioOrderByDataHoraDesc(usuario.get());
        return ResponseEntity.ok(historico);
    }

    @GetMapping("/usuario/{usuarioId}/recente")
    public ResponseEntity<List<HistoricoConversa>> getHistoricoRecenteByUsuario(@PathVariable Long usuarioId) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        List<HistoricoConversa> historico = historicoConversaRepository.findTop10ByUsuarioOrderByDataHoraDesc(usuario.get());
        return ResponseEntity.ok(historico);
    }

    @PostMapping
    public ResponseEntity<HistoricoConversa> saveHistoricoConversa(@RequestBody HistoricoConversa historicoConversa) {
        HistoricoConversa historicoSalvo = historicoConversaRepository.save(historicoConversa);
        return ResponseEntity.ok(historicoSalvo);
    }
}