package com.australiarecycling.service;

import com.australiarecycling.dto.CouncilDetailDto;
import com.australiarecycling.dto.CouncilDto;
import com.australiarecycling.model.Council;
import com.australiarecycling.model.CouncilMaterial;
import com.australiarecycling.repository.CouncilRepository;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CouncilService {

  private final CouncilRepository councilRepository;

  public Page<CouncilDto> findAll(Pageable pageable) {
    return councilRepository.findAll(pageable).map(this::toDto);
  }

  public Page<CouncilDto> findByState(String state, Pageable pageable) {
    return councilRepository.findByState(state, pageable).map(this::toDto);
  }

  public Optional<CouncilDetailDto> findBySlug(String slug) {
    return councilRepository.findBySlug(slug).map(this::toDetailDto);
  }

  private CouncilDto toDto(Council council) {
    return new CouncilDto(
        council.getId(),
        council.getName(),
        council.getSlug(),
        council.getState(),
        council.getWebsite(),
        council.getRecyclingInfoUrl(),
        council.getDescription());
  }

  private CouncilDetailDto toDetailDto(Council council) {
    Map<String, List<CouncilDetailDto.MaterialBinInfo>> materialsByBinType =
        council.getCouncilMaterials().stream()
            .collect(
                Collectors.groupingBy(
                    cm -> cm.getBinType().name(),
                    Collectors.mapping(this::toMaterialBinInfo, Collectors.toList())));

    return new CouncilDetailDto(
        council.getId(),
        council.getName(),
        council.getSlug(),
        council.getState(),
        council.getWebsite(),
        council.getRecyclingInfoUrl(),
        council.getDescription(),
        materialsByBinType);
  }

  private CouncilDetailDto.MaterialBinInfo toMaterialBinInfo(CouncilMaterial cm) {
    return new CouncilDetailDto.MaterialBinInfo(
        cm.getMaterial().getId(),
        cm.getMaterial().getName(),
        cm.getMaterial().getSlug(),
        cm.getMaterial().getCategory(),
        cm.getInstructions(),
        cm.getNotes());
  }
}
