package com.australiarecycling.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.australiarecycling.dto.CouncilDetailDto;
import com.australiarecycling.dto.CouncilDto;
import com.australiarecycling.service.CouncilService;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(CouncilController.class)
class CouncilControllerTest {

  @Autowired private MockMvc mockMvc;

  @MockBean private CouncilService councilService;

  @Test
  void listCouncils_shouldReturnPageOfCouncils() throws Exception {
    CouncilDto council =
        new CouncilDto(
            1L,
            "City of Sydney",
            "city-of-sydney",
            "NSW",
            "https://www.cityofsydney.nsw.gov.au",
            null,
            "Sydney council");
    Page<CouncilDto> page = new PageImpl<>(List.of(council));
    when(councilService.findAll(any(Pageable.class))).thenReturn(page);

    mockMvc
        .perform(get("/api/v1/councils"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content[0].name").value("City of Sydney"))
        .andExpect(jsonPath("$.content[0].slug").value("city-of-sydney"))
        .andExpect(jsonPath("$.content[0].state").value("NSW"));
  }

  @Test
  void listCouncils_withStateFilter_shouldReturnFilteredResults() throws Exception {
    CouncilDto council =
        new CouncilDto(
            1L,
            "City of Melbourne",
            "city-of-melbourne",
            "VIC",
            "https://www.melbourne.vic.gov.au",
            null,
            "Melbourne council");
    Page<CouncilDto> page = new PageImpl<>(List.of(council));
    when(councilService.findByState(eq("VIC"), any(Pageable.class))).thenReturn(page);

    mockMvc
        .perform(get("/api/v1/councils").param("state", "VIC"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content[0].state").value("VIC"));
  }

  @Test
  void getCouncil_shouldReturnCouncilDetail() throws Exception {
    CouncilDetailDto detail =
        new CouncilDetailDto(
            1L,
            "City of Sydney",
            "city-of-sydney",
            "NSW",
            "https://www.cityofsydney.nsw.gov.au",
            null,
            "Sydney council",
            Map.of(
                "RECYCLING",
                List.of(
                    new CouncilDetailDto.MaterialBinInfo(
                        1L, "Paper", "paper", "Paper & Cardboard", "Place in yellow bin", null))));
    when(councilService.findBySlug("city-of-sydney")).thenReturn(Optional.of(detail));

    mockMvc
        .perform(get("/api/v1/councils/city-of-sydney"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.name").value("City of Sydney"))
        .andExpect(jsonPath("$.materialsByBinType.RECYCLING[0].materialName").value("Paper"));
  }

  @Test
  void getCouncil_notFound_shouldReturn404() throws Exception {
    when(councilService.findBySlug("nonexistent")).thenReturn(Optional.empty());

    mockMvc.perform(get("/api/v1/councils/nonexistent")).andExpect(status().isNotFound());
  }
}
