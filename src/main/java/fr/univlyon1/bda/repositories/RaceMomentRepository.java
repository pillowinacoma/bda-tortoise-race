package fr.univlyon1.bda.repositories;

import fr.univlyon1.bda.modele.RaceMoment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface RaceMomentRepository extends JpaRepository<RaceMoment, String> {

}
