package com.australiarecycling.service;

import com.australiarecycling.dto.MaterialDto;
import com.australiarecycling.model.Material;
import com.australiarecycling.repository.MaterialRepository;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MaterialService {

  private final MaterialRepository materialRepository;

  public List<MaterialDto> findAll() {
    return materialRepository.findAll().stream().map(this::toDto).toList();
  }

  public Optional<MaterialDto> findBySlug(String slug) {
    return materialRepository.findBySlug(slug).map(this::toDto);
  }

  public List<MaterialDto> findByCategory(String category) {
    return materialRepository.findByCategory(category).stream().map(this::toDto).toList();
  }

  private MaterialDto toDto(Material material) {
    return new MaterialDto(
        material.getId(),
        material.getName(),
        material.getSlug(),
        material.getCategory(),
        material.getDescription());
  }
}
