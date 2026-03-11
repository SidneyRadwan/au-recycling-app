package com.australiarecycling.dto;

import java.util.List;
import java.util.Map;

public record CouncilDetailDto(
        Long id,
        String name,
        String slug,
        String state,
        String website,
        String recyclingInfoUrl,
        String description,
        Map<String, List<MaterialBinInfo>> materialsByBinType
) {
    public record MaterialBinInfo(
            Long materialId,
            String materialName,
            String materialSlug,
            String category,
            String instructions,
            String notes
    ) {}
}
