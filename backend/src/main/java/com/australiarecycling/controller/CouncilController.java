package com.australiarecycling.controller;

import com.australiarecycling.dto.CouncilDetailDto;
import com.australiarecycling.dto.CouncilDto;
import com.australiarecycling.service.CouncilService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/councils")
public class CouncilController {

  private final CouncilService councilService;

  public CouncilController(CouncilService councilService) {
    this.councilService = councilService;
  }

  @GetMapping
  public Page<CouncilDto> listCouncils(
      @RequestParam(required = false) String state, @PageableDefault(size = 20) Pageable pageable) {
    if (state != null && !state.isBlank()) {
      return councilService.findByState(state, pageable);
    }
    return councilService.findAll(pageable);
  }

  @GetMapping("/{slug}")
  public ResponseEntity<CouncilDetailDto> getCouncil(@PathVariable String slug) {
    return councilService
        .findBySlug(slug)
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity.notFound().build());
  }
}
