package br.edu.ibmec.services;
import br.edu.ibmec.dto.historicoconversadto;

import java.util.List;
import java.util.Optional;

public interface historicoconversaservices {

    List<historicoconversadto> obterTodasConversas();
    Optional<historicoconversadto> obterConversaPorId(Long id);
    historicoconversadto salvarConversa(historicoconversadto conversa);
    historicoconversadto atualizarConversa(Long id, historicoconversadto conversa);
    void deletarConversa(Long id);

}
