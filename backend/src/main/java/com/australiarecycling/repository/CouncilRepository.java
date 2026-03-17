package com.australiarecycling.repository;

import com.australiarecycling.model.Council;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface CouncilRepository extends JpaRepository<Council, Long> {

  Optional<Council> findBySlug(String slug);

  Page<Council> findByState(String state, Pageable pageable);

  @Query("SELECT c FROM Council c WHERE LOWER(c.name) LIKE LOWER(CONCAT('%', :query, '%'))")
  List<Council> searchByName(@Param("query") String query, Pageable pageable);
}
