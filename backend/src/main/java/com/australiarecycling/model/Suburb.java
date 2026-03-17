package com.australiarecycling.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "suburbs")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Suburb {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, length = 10)
  private String postcode;

  @Column(nullable = false, length = 10)
  private String state;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "council_id")
  private Council council;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  @PrePersist
  protected void onCreate() {
    createdAt = LocalDateTime.now();
  }
}
