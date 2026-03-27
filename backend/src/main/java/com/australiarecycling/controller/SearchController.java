package com.australiarecycling.controller;

import com.australiarecycling.dto.SearchResultDto;
import com.australiarecycling.service.SearchService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/search")
public class SearchController {

  private final SearchService searchService;

  public SearchController(SearchService searchService) {
    this.searchService = searchService;
  }

  @GetMapping
  public SearchResultDto search(@RequestParam String q) {
    return searchService.search(q);
  }
}
