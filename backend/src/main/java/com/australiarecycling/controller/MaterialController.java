package com.australiarecycling.controller;

import com.australiarecycling.dto.MaterialDto;
import com.australiarecycling.service.MaterialService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/materials")
public class MaterialController {

  private final MaterialService materialService;

  public MaterialController(MaterialService materialService) {
    this.materialService = materialService;
  }

  @GetMapping
  public List<MaterialDto> listMaterials(@RequestParam(required = false) String category) {
    if (category != null && !category.isBlank()) {
      return materialService.findByCategory(category);
    }
    return materialService.findAll();
  }

  @GetMapping("/{slug}")
  public ResponseEntity<MaterialDto> getMaterial(@PathVariable String slug) {
    return materialService
        .findBySlug(slug)
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity.notFound().build());
  }
}
