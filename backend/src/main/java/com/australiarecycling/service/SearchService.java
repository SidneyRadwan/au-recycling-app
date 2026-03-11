package com.australiarecycling.service;

import com.australiarecycling.dto.CouncilDto;
import com.australiarecycling.dto.MaterialDto;
import com.australiarecycling.dto.SearchResultDto;
import com.australiarecycling.model.Council;
import com.australiarecycling.model.Material;
import com.australiarecycling.model.Suburb;
import com.australiarecycling.repository.CouncilRepository;
import com.australiarecycling.repository.MaterialRepository;
import com.australiarecycling.repository.SuburbRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SearchService {

    private final CouncilRepository councilRepository;
    private final SuburbRepository suburbRepository;
    private final MaterialRepository materialRepository;

    public SearchResultDto search(String query) {
        if (query == null || query.trim().isEmpty()) {
            return new SearchResultDto(List.of(), List.of(), List.of());
        }

        String trimmedQuery = query.trim();

        List<CouncilDto> councils = councilRepository.searchByName(trimmedQuery).stream()
                .map(this::toCouncilDto)
                .toList();

        List<SearchResultDto.SuburbResult> suburbs;
        if (trimmedQuery.matches("\\d+")) {
            suburbs = suburbRepository.searchByPostcode(trimmedQuery).stream()
                    .map(this::toSuburbResult)
                    .toList();
        } else {
            suburbs = suburbRepository.searchByName(trimmedQuery).stream()
                    .map(this::toSuburbResult)
                    .toList();
        }

        List<MaterialDto> materials = materialRepository.searchByName(trimmedQuery).stream()
                .map(this::toMaterialDto)
                .toList();

        return new SearchResultDto(councils, suburbs, materials);
    }

    private CouncilDto toCouncilDto(Council council) {
        return new CouncilDto(
                council.getId(),
                council.getName(),
                council.getSlug(),
                council.getState(),
                council.getWebsite(),
                council.getRecyclingInfoUrl(),
                council.getDescription()
        );
    }

    private SearchResultDto.SuburbResult toSuburbResult(Suburb suburb) {
        return new SearchResultDto.SuburbResult(
                suburb.getId(),
                suburb.getName(),
                suburb.getPostcode(),
                suburb.getState(),
                suburb.getCouncil() != null ? suburb.getCouncil().getId() : null,
                suburb.getCouncil() != null ? suburb.getCouncil().getName() : null,
                suburb.getCouncil() != null ? suburb.getCouncil().getSlug() : null
        );
    }

    private MaterialDto toMaterialDto(Material material) {
        return new MaterialDto(
                material.getId(),
                material.getName(),
                material.getSlug(),
                material.getCategory(),
                material.getDescription()
        );
    }
}
