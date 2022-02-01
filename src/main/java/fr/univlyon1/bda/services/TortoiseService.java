package fr.univlyon1.bda.services;

import fr.univlyon1.bda.modele.Tortoise;
import fr.univlyon1.bda.repositories.TortoiseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TortoiseService {

    @Autowired
    public TortoiseRepository tr;

    public TortoiseService() {
    }

    public boolean createTortoise(Tortoise t) {
        try {
            tr.save(t);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

}
