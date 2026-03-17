package com.australiarecycling.dto;

public record CouncilDto(
    Long id,
    String name,
    String slug,
    String state,
    String website,
    String recyclingInfoUrl,
    String description) {}
