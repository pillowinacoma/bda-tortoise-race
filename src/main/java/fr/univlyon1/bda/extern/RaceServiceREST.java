package fr.univlyon1.bda.extern;

import fr.univlyon1.bda.modele.RaceMoment;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;


public class RaceServiceREST {

    RestTemplate restTemplate = new RestTemplate();

    public RaceMoment getRaceMoment() throws Exception {
        ResponseEntity<RaceMoment> response
                = restTemplate.getForEntity("http://tortues.ecoquery.os.univ-lyon1.fr/race/tiny", RaceMoment.class);

        return response.getBody();
    }
}
