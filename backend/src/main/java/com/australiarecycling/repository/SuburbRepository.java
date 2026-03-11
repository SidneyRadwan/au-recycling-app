package com.australiarecycling.repository;

import com.australiarecycling.model.Suburb;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SuburbRepository extends JpaRepository<Suburb, Long> {

    List<Suburb> findByCouncilId(Long councilId);

    @Query("SELECT s FROM Suburb s JOIN FETCH s.council WHERE LOWER(s.name) LIKE LOWER(CONCAT('%', :query, '%'))")
    List<Suburb> searchByName(@Param("query") String query);

    @Query("SELECT s FROM Suburb s JOIN FETCH s.council WHERE s.postcode LIKE CONCAT(:postcode, '%')")
    List<Suburb> searchByPostcode(@Param("postcode") String postcode);
}
