package com.australiarecycling.controller;

import com.australiarecycling.dto.SearchResultDto;
import com.australiarecycling.service.SearchService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/search")
@RequiredArgsConstructor
public class SearchController {

    private final SearchService searchService;

    @GetMapping
    public SearchResultDto search(@RequestParam String q) {
        return searchService.search(q);
    }
}
