package fr.univlyon1.bda.repositories;

import fr.univlyon1.bda.modele.Tortoise;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TortoiseRepository extends JpaRepository<Tortoise, String>{

}
