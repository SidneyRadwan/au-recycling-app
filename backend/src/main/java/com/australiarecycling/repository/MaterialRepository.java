package com.australiarecycling.repository;

import com.australiarecycling.model.Material;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface MaterialRepository extends JpaRepository<Material, Long> {

  Optional<Material> findBySlug(String slug);

  List<Material> findByCategory(String category);

  @Query("SELECT m FROM Material m WHERE LOWER(m.name) LIKE LOWER(CONCAT('%', :query, '%'))")
  List<Material> searchByName(@Param("query") String query, Pageable pageable);
}
