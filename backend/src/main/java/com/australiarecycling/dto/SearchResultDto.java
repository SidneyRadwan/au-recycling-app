package com.australiarecycling.dto;

import java.util.List;

public record SearchResultDto(
        List<CouncilDto> councils,
        List<SuburbResult> suburbs,
        List<MaterialDto> materials
) {
    public record SuburbResult(
            Long id,
            String name,
            String postcode,
            String state,
            Long councilId,
            String councilName,
            String councilSlug
    ) {}
}
